require 'net/http'

module Docstore
  class DocstoreHTTP
    def initialize(url)
      m = %r{http://([\w\d\.]+):(\d+)(/.*)?}.match(url)
      host, port, @prefix_path = m[1], m[2].to_i, m[3]
      if @prefix_path == nil
        @prefix_path = ''
      end
      @http = Net::HTTP.new(host, port)
      @cache = {}
    end

    def wait_until_up(timeout=5)
      return nil # not implemented
    end

    def wait_and_get(path, timeout=5)
      return nil # not implemented
    end

    def put(data, path, content_type=nil)
      path = @prefix_path + path
      if content_type == nil
        content_type = Docstore::mime_from_path(path)
      end
      @http.send_request('PUT', path, data, {'Content-Type' => content_type})
    end

    def get(path)
      path = @prefix_path + path
      if not @cache.has_key?(path)
        fill_cache(path)
      end
      return @cache[path]
    end

    def fill_cache(path)
      response = @http.get(path)
      if response.code == "200"
        @cache[path] = response.body
      end
    end
  end

  def Docstore.connect(url)
    DocstoreHTTP.new(url)
  end

  MIME_TYPES = {'html' => 'text/html',
                'json' => 'application/json',
                'md'   => 'text/x-markdown',
                'py'   => 'text/x-python',
                'rb'   => 'text/x-ruby',
                'txt'  => 'text/plain'}
  MIME_TYPES.default = 'text/plain'

  def Docstore.mime_from_path(path)
    m = %r{\.(\w+)$}.match(path)
    if m == nil
      MIME_TYPES.default
    else
      MIME_TYPES[m[1]]
    end
  end
end
